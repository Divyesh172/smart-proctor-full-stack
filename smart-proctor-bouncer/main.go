package main

import (
	"bytes"
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

	// Thread-safe map to track active connections
	activeClients   = make(map[string]*websocket.Conn)
	clientsMutex    sync.RWMutex

	upgrader = websocket.Upgrader{
		ReadBufferSize:  1024,
		WriteBufferSize: 1024,
		CheckOrigin: func(r *http.Request) bool {
			origin := r.Header.Get("Origin")
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

type Claims struct {
	Sub  string `json:"sub"` // Student ID
	Role string `json:"role"`
	jwt.RegisteredClaims
}

type Heartbeat struct {
	StudentID  string  `json:"student_id"`
	FlightTime float64 `json:"flight_time"` // ms between keys
	DwellTime  float64 `json:"dwell_time"`  // ms key held down
}

type Alert struct {
	Status  string `json:"status"`
	Message string `json:"message"`
}

// ---------------------------------------------------------
// 3. INITIALIZATION
// ---------------------------------------------------------
func init() {
	secret := os.Getenv("SECRET_KEY")
	if secret == "" {
		// Fallback for local testing if env not set
		log.Println("⚠️  WARNING: SECRET_KEY not set. Using default for dev.")
		secret = "change_this_to_a_super_secret_random_string_for_tuesday_demo_only"
	}
	jwtKey = []byte(secret)

	origins := os.Getenv("ALLOWED_ORIGINS")
	if origins != "" {
		allowedOrigins = strings.Split(origins, ",")
	}

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

	// B. VERIFY JWT
	claims := &Claims{}
	token, err := jwt.ParseWithClaims(tokenString, claims, func(token *jwt.Token) (interface{}, error) {
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

	studentID := claims.Sub
	clientsMutex.Lock()
	activeClients[studentID] = ws
	clientsMutex.Unlock()

	log.Printf("✅ Secure Link Established: Student %s", studentID)

	// --- SESSION STATS TRACKING ---
	var baselineFlightTime float64 = 150.0 // Mock baseline for now
	var sessionTotalFlightTime float64 = 0.0
	var sessionKeystrokes int = 0

	// D. CLEANUP & SAVE ON DISCONNECT
	defer func() {
		clientsMutex.Lock()
		delete(activeClients, studentID)
		clientsMutex.Unlock()

		// SAVE DNA: If we gathered enough data, send it to Python
		if sessionKeystrokes > 5 {
			avg := sessionTotalFlightTime / float64(sessionKeystrokes)
			go saveUserBaselineToBackend(studentID, avg)
		}

		log.Printf("🔌 Disconnected: Student %s", studentID)
	}()

	// E. ANALYSIS LOOP
	for {
		var beat Heartbeat
		err := ws.ReadJSON(&beat)
		if err != nil {
			break
		}

		// 1. UPDATE STATS
		if beat.FlightTime > 0 && beat.FlightTime < 2000 { // Ignore pauses > 2s
			sessionTotalFlightTime += beat.FlightTime
			sessionKeystrokes++
		}

		// 2. BOT DETECTION (Superhuman Speed)
		if beat.FlightTime < 10.0 && beat.FlightTime > 0 {
			log.Printf("🚨 BOT DETECTED: Student %s (Speed: %.2fms)", studentID, beat.FlightTime)
			alert := Alert{Status: "TERMINATE", Message: "Automated typing pattern detected."}
			ws.WriteJSON(alert)
			break
		}

		// 3. BIOMETRIC MISMATCH
		deviation := math.Abs(beat.FlightTime - baselineFlightTime)
		if deviation > 80.0 {
			log.Printf("⚠️  Rhythm Mismatch: Student %s (Dev: %.2fms)", studentID, deviation)
		}
	}
}

// --- NEW: SENDS DATA TO PYTHON BACKEND ---
func saveUserBaselineToBackend(studentID string, avgFlightTime float64) {
	payload := map[string]interface{}{
		"user_id":         studentID,
		"new_flight_time": avgFlightTime,
	}

	jsonBody, _ := json.Marshal(payload)

	// Determine Backend URL (Localhost vs Docker)
	backendURL := os.Getenv("BACKEND_URL")
	if backendURL == "" {
		backendURL = "http://localhost:8000" // Default for local testing
	}

	url := fmt.Sprintf("%s/api/v1/exam/internal/update-baseline", backendURL)
	resp, err := http.Post(url, "application/json", bytes.NewBuffer(jsonBody))
	if err != nil {
		log.Printf("❌ Failed to contact Backend: %v", err)
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode == 200 {
		log.Printf("🧬 DNA Saved for User %s: %.2fms", studentID, avgFlightTime)
	} else {
		log.Printf("❌ Backend rejected update: Status %d", resp.StatusCode)
	}
}

// ---------------------------------------------------------
// 5. SERVER SETUP
// ---------------------------------------------------------
func handleHealth(w http.ResponseWriter, r *http.Request) {
	clientsMutex.RLock()
	count := len(activeClients)
	clientsMutex.RUnlock()
	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, `{"status": "healthy", "active_connections": %d}`, count)
}

func main() {
	http.HandleFunc("/ws", handleConnections)
	http.HandleFunc("/health", handleHealth)

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	server := &http.Server{Addr: ":" + port, Handler: nil}

	go func() {
		fmt.Printf("🛡️  VerifAI Bouncer Running on Port %s\n", port)
		if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Listen Error: %s\n", err)
		}
	}()

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	server.Shutdown(ctx)
	log.Println("Bouncer Exited Properly")
}