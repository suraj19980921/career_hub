import { Route, Routes } from 'react-router-dom'

import HomePage from '../pages/HomePage'
import JobsPage from '../pages/JobsPage'

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/jobs" element={<JobsPage />} />
      <Route path="*" element={<HomePage />} />
    </Routes>
  )
}

export default AppRoutes
