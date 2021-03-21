import Vue from 'vue'

export const EventBus = new Vue()

export function isValidJwt (jwt) {
  return !(!jwt || jwt.split('.').length < 3)
}