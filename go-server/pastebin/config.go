// config.go
package main

import (
	"log"
	"os"
	"strconv"

	"gopkg.in/yaml.v3"
)

type Config struct {
	Port         string `yaml:"port"`
	DBPath       string `yaml:"db_path"`
	MaxPasteSize int    `yaml:"max_paste_size"`
	DefaultTTL   int    `yaml:"default_ttl"`
}

func LoadConfig() Config {
	config := Config{
		Port:         "8080",
		DBPath:       "./pastebin.db",
		MaxPasteSize: 1024 * 1024, // 1MB
		DefaultTTL:   86400,       // 24 hours
	}

	if err := loadFromYAML("config.yaml", &config); err != nil {
		log.Printf("No config.yaml found or error reading it, using defaults: %v", err)
	}

	if port := os.Getenv("PORT"); port != "" {
		config.Port = port
	}
	if dbPath := os.Getenv("DB_PATH"); dbPath != "" {
		config.DBPath = dbPath
	}
	if maxSize := os.Getenv("MAX_PASTE_SIZE"); maxSize != "" {
		if size, err := strconv.Atoi(maxSize); err == nil {
			config.MaxPasteSize = size
		}
	}
	if ttl := os.Getenv("DEFAULT_TTL"); ttl != "" {
		if t, err := strconv.Atoi(ttl); err == nil {
			config.DefaultTTL = t
		}
	}

	return config
}

func loadFromYAML(filename string, config *Config) error {
	data, err := os.ReadFile(filename)
	if err != nil {
		return err
	}

	return yaml.Unmarshal(data, config)
}

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

func getEnvInt(key string, defaultValue int) int {
	if value := os.Getenv(key); value != "" {
		if intVal, err := strconv.Atoi(value); err == nil {
			return intVal
		}
	}
	return defaultValue
}
