import api from './api'

export const getHomepage = () => api.get('/v1/homepage/')
export const searchHomepage = (query) => api.get('/v1/search/', { params: { q: query } })
export const subscribeNewsletter = (email) => api.post('/v1/newsletter/subscribe/', { email })
