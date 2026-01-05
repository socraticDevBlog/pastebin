// main.go
package main

import (
	"fmt"
	"log"
)

func main() {
	config := LoadConfig()
	db, err := initDB(config.DBPath)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	log.Println(fmt.Sprintf("Database %s ready to be used!", config.DBPath))
}
