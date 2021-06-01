package model

import "go.mongodb.org/mongo-driver/bson/primitive"

type BaseRestaurant struct {
	ID           primitive.ObjectID `json:"id,omitempty" bson:"_id"`
	ManagerEmail string             `json:"manager_email" bson:"manager_email"`

	Name         string  `json:"name" bson:"name"`
	WorkingHours string  `json:"working-hours" bson:"working_hours"`
	Region       string  `json:"region" bson:"region"`
	Address      string  `json:"address" bson:"address"`
	Credit       float64 `json:"credit" bson:"credit"`

	Orders *[]primitive.ObjectID `json:"orders" bson:"orders"`
}

type Restaurant struct {
	BaseManager
	ID primitive.ObjectID `json:"id,omitempty" bson:"_id"`

	Name         string  `json:"name" bson:"name"`
	WorkingHours string  `json:"working-hours" bson:"working_hours"`
	Region       string  `json:"region" bson:"region"`
	Address      string  `json:"address" bson:"address"`
	Credit       float64 `json:"credit" bson:"credit"`

	Foods  *[]primitive.ObjectID `json:"foods" bson:"foods"`
	Orders *[]primitive.ObjectID `json:"orders" bson:"orders"`
}
