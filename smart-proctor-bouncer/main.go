package main

import (
	"fmt"
	"log"
	"math"
	"net/http"

	"github.com/golang-jwt/jwt/v5"
	"github.com/gorilla/websocket"
)

// ---------------------------------------------------------
// 1. CONFIGURATION
// ---------------------------------------------------------
var (
	// MUST match the SECRET_KEY in your Python .env
	jwtKey = []byte("change_this_to_a_super_secret_random_string_for_tuesday_demo_only")

	upgrader = websocket.Upgrader{
		CheckOrigin: func(r *http.Request) bool {
			return true // Allow all for demo
		},
	}
)

// ---------------------------------------------------------
// 2. DATA STRUCTURES
// ---------------------------------------------------------

type Claims struct {
	Sub  string `json:"sub"`
	Role string `json:"role"`
	jwt.RegisteredClaims
}

type Heartbeat struct {
	StudentID  string  `json:"student_id"`
	FlightTime float64 `json:"flight_time"`
	DwellTime  float64 `json:"dwell_time"`
}

type Alert struct {
	Status  string `json:"status"`
	Message string `json:"message"`
}

// ---------------------------------------------------------
// 3. LOGIC
// ---------------------------------------------------------

func handleConnections(w http.ResponseWriter, r *http.Request) {
	// A. Validate Token
	tokenString := r.URL.Query().Get("token")
	claims := &Claims{}

	token, err := jwt.ParseWithClaims(tokenString, claims, func(token *jwt.Token) (interface{}, error) {
		return jwtKey, nil
	})

	if err != nil || !token.Valid {
		log.Printf("⛔ Security Alert: Invalid Token")
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}

	// B. Upgrade Connection
	ws, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Fatal(err)
	}
	defer ws.Close()

	log.Printf("✅ Connection: Student %s", claims.Sub)

	var baselineFlightTime float64 = 150.0

	// C. Loop
	for {
		var beat Heartbeat
		// Gorilla WebSocket handles the JSON unmarshalling here automatically
		err := ws.ReadJSON(&beat)
		if err != nil {
			log.Printf("⚠️ Connection Lost: Student %s", claims.Sub)
			break
		}

		// Analysis
		if beat.FlightTime < 10.0 {
			log.Printf("🚨 BOT DETECTED: Student %s (Speed: %.2fms)", claims.Sub, beat.FlightTime)
			alert := Alert{Status: "TERMINATE", Message: "Bot detected."}
			ws.WriteJSON(alert)
			break
		}

		deviation := math.Abs(beat.FlightTime - baselineFlightTime)
		if deviation > 80.0 {
			log.Printf("👀 Suspicious Rhythm: Student %s", claims.Sub)
		} else {
			// Adaptive Learning
			baselineFlightTime = (baselineFlightTime + beat.FlightTime) / 2
			log.Printf("❤️ Heartbeat: Student %s | Rhythm: Stable", claims.Sub)
		}
	}
}

func main() {
	http.HandleFunc("/ws", handleConnections)

	port := "8080"
	fmt.Println("------------------------------------------------")
	fmt.Println("🛡️  VerifAI Bouncer (Go Service) Running")
	fmt.Println("🚀 Port:", port)
	fmt.Println("------------------------------------------------")

	err := http.ListenAndServe(":"+port, nil)
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}