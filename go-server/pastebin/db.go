// db.go
package main

import (
	"database/sql"
	"fmt"
	"log"

	_ "modernc.org/sqlite"
)

func initDB(filepath string) (*sql.DB, error) {
	db, err := sql.Open("sqlite", filepath)
	if err != nil {
		log.Println(fmt.Sprintf("Database %s already exists. Exiting", filepath))
		return nil, err
	}

	if err := db.Ping(); err != nil {
		log.Println(fmt.Sprintf("Failed to connect %s Database. Exiting.", filepath))
		return nil, err
	}

	if err := createSchema(db); err != nil {
		log.Println(fmt.Sprintf("Schema already set for %s database. Exiting.", filepath))
		return nil, err
	}

	return db, nil
}

func createSchema(db *sql.DB) error {
	schema := `
    CREATE TABLE IF NOT EXISTS pastes (
        id TEXT PRIMARY KEY,
        client_id TEXT NOT NULL,
        content TEXT NOT NULL,
        ttl INTEGER NOT NULL,
        created_at INTEGER NOT NULL,
        expires_at INTEGER,
        view_count INTEGER DEFAULT 0
    );
    
    CREATE INDEX IF NOT EXISTS idx_expires_at ON pastes(expires_at);
    CREATE INDEX IF NOT EXISTS idx_client_id ON pastes(client_id);
    `

	_, err := db.Exec(schema)
	return err
}
