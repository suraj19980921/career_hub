import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'

function Brand(){return <Link className="brand" to="/"><img className="brand-mark-image" src="/assets/brand-mark.svg" alt=""/><span><strong>GovCareer <i>Hub</i></strong><small>Your Path to a Secure Future</small></span></Link>}
export default function Header(){
 const [open,setOpen]=useState(false),location=useLocation(); const nav=[['Jobs','/jobs'],['Exams','/'],['Results','/'],['Admit Cards','/'],['Answer Keys','/'],['Syllabus','/'],['News','/']]
 return <header className="site-header"><div className="page-shell nav-wrap"><button className="mobile-menu" aria-label="Toggle navigation" aria-expanded={open} onClick={()=>setOpen(!open)}>☰</button><Brand/><nav className={open?'nav-links nav-open':'nav-links'} aria-label="Main navigation">{nav.map(([item,path],i)=><Link className={location.pathname===path&&path!=='/'?'active':''} key={item} to={path} onClick={()=>setOpen(false)}>{item}{i<2&&<span className="chevron">⌄</span>}</Link>)}</nav><div className="nav-actions"><button className="round-button" aria-label="Search">⌕</button><Link className="login-button" to="/login">Login</Link><Link className="register-button" to="/register">Register</Link></div><button className="mobile-bell" aria-label="Notifications">♧</button></div></header>
}
