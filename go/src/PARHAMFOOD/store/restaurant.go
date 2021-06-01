package store

import "go.mongodb.org/mongo-driver/mongo"

type RestaurantStore struct {
	db *mongo.Collection
}

func NewRestaurantStore(db *mongo.Collection) *RestaurantStore {
	return &RestaurantStore{
		db: db,
	}
}
