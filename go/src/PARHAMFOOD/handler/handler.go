package handler

import (
	"PARHAMFOOD/modelInterfaces"
)

type (
	Handler struct {
		userStore            modelInterfaces.UserStore
		restaurantStore      modelInterfaces.RestaurantStore
		foodsStore           modelInterfaces.FoodStore
		ordersStore          modelInterfaces.OrderStore
		commentsStore        modelInterfaces.CommentStore
		managerCommentsStore modelInterfaces.ManagerCommentStore
	}
)

func NewHandler(userStore modelInterfaces.UserStore, restaurantStore modelInterfaces.RestaurantStore, foodsStore modelInterfaces.FoodStore, ordersStore modelInterfaces.OrderStore, commentsStore modelInterfaces.CommentStore, managerCommentsStore modelInterfaces.ManagerCommentStore) (handler *Handler) {
	return &Handler{
		userStore:            userStore,
		restaurantStore:      restaurantStore,
		foodsStore:           foodsStore,
		ordersStore:          ordersStore,
		commentsStore:        commentsStore,
		managerCommentsStore: managerCommentsStore,
	}
}

func NewHandlerNotPointer(userStore modelInterfaces.UserStore, restaurantStore modelInterfaces.RestaurantStore, foodsStore modelInterfaces.FoodStore, ordersStore modelInterfaces.OrderStore, commentsStore modelInterfaces.CommentStore, managerCommentsStore modelInterfaces.ManagerCommentStore) (handler *Handler) {
	var h *Handler
	h.userStore = userStore
	h.restaurantStore = restaurantStore
	h.foodsStore = foodsStore
	h.ordersStore = ordersStore
	h.commentsStore = commentsStore
	h.managerCommentsStore = managerCommentsStore
	return h
}
