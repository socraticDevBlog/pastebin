// pastebin.go
package main

type Paste struct {
	ID        string `json:"id" db:"id"`
	ClientID  string `json:"clientId" db:"client_id"`
	Content   string `json:"content" db:"content"`
	Language  string `json:"language,omitempty" db:"language"`
	TTL       int    `json:"ttl" db:"ttl"`
	CreatedAt int64  `json:"createdAt" db:"created_at"`
	ExpiresAt *int64 `json:"expiresAt,omitempty" db:"expires_at"` // pointer for NULL
	ViewCount int    `json:"viewCount,omitempty" db:"view_count"`
}
