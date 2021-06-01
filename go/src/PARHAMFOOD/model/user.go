package model

import "go.mongodb.org/mongo-driver/bson/primitive"

type User struct {
	Name        string `json:"name" bson:"name"`
	PhoneNumber string `json:"phone_number" bson:"phone_number"`
	Email       string `json:"email" bson:"email"`
	Password    string `json:"password" bson:"password"`

	Orders *[]primitive.ObjectID `json:"orders" bson:"orders"`
}
