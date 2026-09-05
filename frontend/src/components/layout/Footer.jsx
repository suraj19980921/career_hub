import { useState } from 'react'

const columns = [
  ['Quick Links', 'About Us', 'Contact Us', 'Privacy Policy', 'Terms & Conditions', 'Sitemap'],
  ['Important Links', 'Jobs', 'Exams', 'Results', 'Admit Cards', 'Answer Keys'],
  ['Resources', 'Syllabus', 'Study Material', 'Current Affairs', 'Exam Calendar', 'Government Websites'],
]

export default function Footer({ onSubscribe }) {
  const [message, setMessage] = useState('')
  const [submitting, setSubmitting] = useState(false)
  async function submit(event) {
    event.preventDefault()
    const email = new FormData(event.currentTarget).get('email')
    setSubmitting(true); setMessage('')
    try { await onSubscribe(email); event.currentTarget.reset(); setMessage('Subscribed successfully.') }
    catch (error) { setMessage(error.response?.data?.email?.[0] || 'Unable to subscribe. Please try again.') }
    finally { setSubmitting(false) }
  }
  return <footer className="site-footer"><div className="page-shell footer-content">
    <div className="footer-brand"><div className="brand footer-logo"><span className="brand-mark">◆</span><strong>GovCareer Hub</strong></div><p>Your trusted companion for government jobs, exams, results and career updates.</p><div className="socials" aria-label="Social media"><span>f</span><span>𝕏</span><span>◉</span><span>▶</span></div></div>
    {columns.map(([heading, ...links]) => <div className="footer-column" key={heading}><h2>{heading}</h2>{links.map(link => <a href="#footer" key={link}>{link}</a>)}</div>)}
    <form className="newsletter" onSubmit={submit}><h2>Newsletter</h2><p>Get the latest updates in your inbox.</p><label className="visually-hidden" htmlFor="email">Email address</label><div><input id="email" name="email" type="email" placeholder="Enter your email" required /><button disabled={submitting}>{submitting ? 'Saving…' : 'Subscribe'}</button></div>{message && <small className="newsletter-message">{message}</small>}</form>
  </div><div className="copyright">© 2024 GovCareer Hub. All Rights Reserved.</div></footer>
}
