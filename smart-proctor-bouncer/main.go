package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"math"
	"net/http"
	"os"
	"os/signal"
	"strings"
	"sync"
	"syscall"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"github.com/gorilla/websocket"
)

// ---------------------------------------------------------
// 1. CONFIGURATION & GLOBALS
// ---------------------------------------------------------
var (
	jwtKey        []byte
	allowedOrigins []string

	// Thread-safe map to track active connections (for monitoring)
	activeClients   = make(map[string]*websocket.Conn)
	clientsMutex    sync.RWMutex

	upgrader = websocket.Upgrader{
		ReadBufferSize:  1024,
		WriteBufferSize: 1024,
		// SECURITY: Origin Check
		CheckOrigin: func(r *http.Request) bool {
			origin := r.Header.Get("Origin")
			// If no allowed origins configured, allow all (Dev Mode)
			if len(allowedOrigins) == 0 {
				return true
			}
			for _, allowed := range allowedOrigins {
				if origin == allowed {
					return true
				}
			}
			log.Printf("⛔ Security Block: Invalid Origin %s", origin)
			return false
		},
	}
)

// ---------------------------------------------------------
// 2. DATA STRUCTURES
// ---------------------------------------------------------

// Claims matches the Python JWT payload
type Claims struct {
	Sub  string `json:"sub"` // Student ID
	Role string `json:"role"`
	jwt.RegisteredClaims
}

// Heartbeat comes from the Frontend (useKeystrokeDNA hook)
type Heartbeat struct {
	StudentID  string  `json:"student_id"`
	FlightTime float64 `json:"flight_time"` // ms between keys
	DwellTime  float64 `json:"dwell_time"`  // ms key held down
}

// Alert goes back to Frontend to trigger "Red Screen"
type Alert struct {
	Status  string `json:"status"`  // "TERMINATE", "WARNING"
	Message string `json:"message"`
}

// ---------------------------------------------------------
// 3. INITIALIZATION
// ---------------------------------------------------------
func init() {
	// A. Load Secret Key (Must match Python Backend)
	secret := os.Getenv("SECRET_KEY")
	if secret == "" {
		log.Fatal("FATAL: SECRET_KEY environment variable is not set. The Bouncer cannot verify tokens.")
	}
	jwtKey = []byte(secret)

	// B. Load Allowed Origins (CORS for WebSockets)
	origins := os.Getenv("ALLOWED_ORIGINS")
	if origins != "" {
		allowedOrigins = strings.Split(origins, ",")
	}

	// Setup standard logging flags
	log.SetFlags(log.Ldate | log.Ltime | log.Lmicroseconds | log.Lshortfile)
}

// ---------------------------------------------------------
// 4. CORE LOGIC
// ---------------------------------------------------------

func handleConnections(w http.ResponseWriter, r *http.Request) {
	// A. EXTRACT TOKEN
	tokenString := r.URL.Query().Get("token")
	if tokenString == "" {
		http.Error(w, "Missing Authentication Token", http.StatusUnauthorized)
		return
	}

	// B. VERIFY JWT (Signature Check)
	claims := &Claims{}
	token, err := jwt.ParseWithClaims(tokenString, claims, func(token *jwt.Token) (interface{}, error) {
		// Ensure the signing method is HMAC (matches Python's HS256)
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
		}
		return jwtKey, nil
	})

	if err != nil || !token.Valid {
		log.Printf("⛔ Security Alert: Invalid Token Attempt from %s", r.RemoteAddr)
		http.Error(w, "Invalid Token", http.StatusUnauthorized)
		return
	}

	// C. UPGRADE TO WEBSOCKET
	ws, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Printf("Upgrade Error: %v", err)
		return
	}
	defer ws.Close()

	// Register Client
	studentID := claims.Sub
	clientsMutex.Lock()
	activeClients[studentID] = ws
	clientsMutex.Unlock()

	log.Printf("✅ Secure Link Established: Student %s (IP: %s)", studentID, r.RemoteAddr)

	defer func() {
		clientsMutex.Lock()
		delete(activeClients, studentID)
		clientsMutex.Unlock()
		log.Printf("🔌 Disconnected: Student %s", studentID)
	}()

	// D. BIOMETRIC ANALYSIS LOOP
	// Baseline profile (Mock: In real app, fetch from Python API or Redis)
	var baselineFlightTime float64 = 150.0

	for {
		var beat Heartbeat
		err := ws.ReadJSON(&beat)
		if err != nil {
			break // Connection closed
		}

		// 1. BOT DETECTION (Superhuman Speed)
		// If flight time is consistently < 10ms, it's a script pasting text.
		if beat.FlightTime < 10.0 && beat.FlightTime > 0 {
			log.Printf("🚨 BOT DETECTED: Student %s (Speed: %.2fms)", studentID, beat.FlightTime)

			alert := Alert{
				Status:  "TERMINATE",
				Message: "Automated typing pattern detected. Exam terminated.",
			}
			ws.WriteJSON(alert)
			break // Kick user
		}

		// 2. BIOMETRIC MISMATCH (Imposter Logic)
		// If typing rhythm deviates by > 80ms from baseline, flag it.
		deviation := math.Abs(beat.FlightTime - baselineFlightTime)

		if deviation > 80.0 {
			// In production, we don't kick immediately, we increment a "Suspicion Score"
			// stored in Redis. For now, we log it.
			log.Printf("⚠️  Rhythm Mismatch: Student %s (Dev: %.2fms)", studentID, deviation)
		} else {
			// Adaptive Learning: Update baseline slightly to account for fatigue
			baselineFlightTime = (baselineFlightTime*0.9) + (beat.FlightTime*0.1)
		}
	}
}

// ---------------------------------------------------------
// 5. HEALTH CHECK (For Kubernetes/Docker)
// ---------------------------------------------------------
func handleHealth(w http.ResponseWriter, r *http.Request) {
	clientsMutex.RLock()
	count := len(activeClients)
	clientsMutex.RUnlock()

	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, `{"status": "healthy", "active_connections": %d}`, count)
}

// ---------------------------------------------------------
// 6. MAIN ENTRY POINT
// ---------------------------------------------------------
func main() {
	// Routes
	http.HandleFunc("/ws", handleConnections)
	http.HandleFunc("/health", handleHealth)

	// Config
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	// Server Configuration
	server := &http.Server{
		Addr:    ":" + port,
		Handler: nil,
	}

	// Run Server in Goroutine
	go func() {
		fmt.Println("------------------------------------------------")
		fmt.Printf("🛡️  VerifAI Bouncer Running on Port %s\n", port)
		fmt.Println("------------------------------------------------")
		if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Listen Error: %s\n", err)
		}
	}()

	// Graceful Shutdown Logic
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit
	log.Println("Shutting down Bouncer...")

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := server.Shutdown(ctx); err != nil {
		log.Fatal("Server Forced Shutdown:", err)
	}

	log.Println("Bouncer Exited Properly")
}