import api from './api'

export const getRecruitments = (params) => api.get('/v1/recruitments/', { params })
export const getRecruitmentStats = () => api.get('/v1/recruitments/stats/')
export const getRecruitmentFilters = () => api.get('/v1/recruitments/filters/')
