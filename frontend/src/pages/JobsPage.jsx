import { useEffect, useRef, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'

import { Icon, JobCard, JobFilters, JobsPagination, JobsStats } from '../components/jobs/JobsParts'
import Footer from '../components/layout/Footer'
import Header from '../components/layout/Header'
import { subscribeNewsletter } from '../services/homepageService'
import { getRecruitmentFilters, getRecruitments, getRecruitmentStats } from '../services/recruitmentService'

const filterKeys = ['search', 'category', 'organization', 'qualification', 'state', 'status', 'date_posted', 'ordering', 'page']

function valuesFromParams(params) {
  return Object.fromEntries(filterKeys.map(key => [key, params.get(key) || '']))
}

export default function JobsPage() {
  const [params, setParams] = useSearchParams()
  const query = params.toString()
  const [draft, setDraft] = useState(() => valuesFromParams(params))
  const [data, setData] = useState(null)
  const [stats, setStats] = useState({})
  const [options, setOptions] = useState({})
  const [error, setError] = useState('')
  const [drawer, setDrawer] = useState(false)
  const [retry, setRetry] = useState(0)
  const searchTimer = useRef(null)

  useEffect(() => setDraft(valuesFromParams(params)), [query])
  useEffect(() => () => clearTimeout(searchTimer.current), [])
  useEffect(() => {
    document.title = 'Government Jobs – Latest Sarkari Jobs | GovCareer Hub'
    let meta = document.querySelector('meta[name="description"]')
    if (!meta) {
      meta = document.createElement('meta')
      meta.name = 'description'
      document.head.appendChild(meta)
    }
    meta.content = 'Browse the latest government jobs in India. Filter jobs by qualification, organization, category, location and application deadline.'
  }, [])
  useEffect(() => {
    getRecruitmentStats().then(response => setStats(response.data))
    getRecruitmentFilters().then(response => setOptions(response.data))
  }, [])
  useEffect(() => {
    let active = true
    setData(null)
    setError('')
    getRecruitments(Object.fromEntries([...params.entries()].filter(([, value]) => value)))
      .then(response => active && setData(response.data))
      .catch(() => active && setError("We couldn't load jobs right now."))
    return () => { active = false }
  }, [query, retry])

  function commitFilters(next) {
    const output = {}
    filterKeys.forEach(key => {
      if (next[key] && key !== 'page') output[key] = next[key]
    })
    setParams(output)
  }

  function changeFilter(key, value) {
    const next = { ...draft, [key]: value }
    setDraft(next)
    clearTimeout(searchTimer.current)
    if (key === 'search') {
      searchTimer.current = setTimeout(() => commitFilters(next), 350)
    } else {
      commitFilters(next)
    }
  }

  function resetFilters() {
    clearTimeout(searchTimer.current)
    setDraft({})
    setParams({})
    setDrawer(false)
  }

  function goToPage(nextPage) {
    const next = new URLSearchParams(params)
    next.set('page', nextPage)
    setParams(next)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const page = Number(params.get('page') || 1)
  const totalPages = Math.max(Math.ceil((data?.count || 0) / 20), 1)
  const resultStart = data?.count ? (page - 1) * 20 + 1 : 0
  const resultEnd = Math.min(page * 20, data?.count || 0)
  const sortControl = <select aria-label="Sort jobs" value={draft.ordering || '-published_at'} onChange={event => changeFilter('ordering', event.target.value)}><option value="-published_at">Latest</option><option value="last_date">Closing Soon</option><option value="-total_vacancies">Highest Vacancies</option></select>

  return <><Header /><main className="jobs-page"><div className="page-shell">
    <nav className="breadcrumb" aria-label="Breadcrumb"><Link to="/">Home</Link><span>›</span><span aria-current="page">Jobs</span></nav>
    <div className="jobs-title"><h1>All Government Jobs</h1><p>Find the latest government job notifications across India.</p></div>
    <div className="mobile-tools"><button onClick={() => setDrawer(true)}><Icon name="filter" /> Filters</button><label><Icon name="sort" />{sortControl}</label></div>
    <div className="jobs-layout"><aside className="desktop-filter"><JobFilters values={draft} options={options} onChange={changeFilter} onReset={resetFilters} /></aside>
      <section className="jobs-results"><JobsStats stats={stats} /><div className="results-toolbar"><p>{data ? `Showing ${resultStart}–${resultEnd} of ${data.count.toLocaleString('en-IN')} jobs` : 'Loading jobs…'}</p><label>Sort By {sortControl}</label></div>
        {!data && !error && <div className="jobs-skeleton" aria-label="Loading jobs">{[1, 2, 3, 4].map(item => <div key={item} />)}</div>}
        {error && <div className="jobs-message" role="alert"><h2>{error}</h2><button onClick={() => setRetry(value => value + 1)}>Try Again</button></div>}
        {data?.results?.length === 0 && <div className="jobs-message"><h2>No jobs found</h2><p>Try changing or clearing some filters.</p><button onClick={resetFilters}>Clear Filters</button></div>}
        <div className="jobs-list">{data?.results?.map(job => <JobCard job={job} key={job.slug} />)}</div>
        <JobsPagination page={page} totalPages={totalPages} onPage={goToPage} />
      </section>
    </div>
  </div></main>
  {drawer && <div className="filter-drawer" role="dialog" aria-modal="true" aria-label="Job filters"><button className="drawer-backdrop" aria-label="Close filters" onClick={() => setDrawer(false)} /><JobFilters mobile values={draft} options={options} onChange={changeFilter} onReset={resetFilters} onClose={() => setDrawer(false)} /></div>}
  <Footer onSubscribe={subscribeNewsletter} /></>
}
