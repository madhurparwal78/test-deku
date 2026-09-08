import { render } from 'preact';
import { useEffect } from 'preact/hooks';
import { usePath, navigate } from './lib/router.js';
import { Link } from './lib/link.jsx';
import { setToken, api } from './lib/api.js';
import { SiteHeader, SiteFooter } from './components/ui.jsx';
import { Home, Product, Technology, About, Careers, News } from './routes/public.jsx';
import { Contact, Privacy, Verify } from './routes/public2.jsx';
import { ConsoleBoard, Intake, RunDetail, Genealogy, RecordScreen, Reconciliation, LotDetail } from './routes/console.jsx';
import { BalancePeriod, BalanceList } from './routes/balance.jsx';
import { Certificates, CertDetail, WizardStep } from './routes/certificates.jsx';
import { Login } from './routes/login.jsx';
import './styles.css';

const t = sessionStorage.getItem('token');
if (t) setToken(t);

function NotFound({ path }) {
  return (
    <div class="layout stack" style="padding-top:4rem">
      <p class="eyebrow">Not found</p>
      <h1 style="font-size:var(--step-h3);line-height:var(--lh-h3)">There is no page at {path}</h1>
      <Link class="button" href="/">Return to the public site</Link>
    </div>
  );
}

function App() {
  const path = usePath();
  const clean = path.split('?')[0].replace(/\/$/, '') || '/';
  const isConsole = clean.startsWith('/console');
  const isVerify = clean.startsWith('/verify/');

  useEffect(() => {
    if (isConsole && !sessionStorage.getItem('token') && clean !== '/login') {
      navigate('/login?next=' + encodeURIComponent(clean), { replace: true });
    }
  }, [isConsole, clean]);

  let page = null;
  if (clean === '/') page = <Home />;
  else if (clean === '/product') page = <Product />;
  else if (clean === '/technology') page = <Technology />;
  else if (clean === '/about') page = <About />;
  else if (clean === '/careers') page = <Careers />;
  else if (clean === '/news') page = <News />;
  else if (clean === '/contact') page = <Contact />;
  else if (clean === '/privacy') page = <Privacy />;
  else if (clean === '/login') page = <Login />;
  else if (isVerify) page = <Verify number={clean.slice('/verify/'.length)} />;
  else if (clean === '/console') page = <ConsoleBoard />;
  else if (clean === '/console/intake') page = <Intake />;
  else if (clean === '/console/record') page = <RecordScreen />;
  else if (clean === '/console/reconciliation') page = <Reconciliation />;
  else if (clean === '/console/certificates') page = <Certificates />;
  else if (clean.startsWith('/console/certificates/new/')) page = <WizardStep step={clean.split('/').pop()} />;
  else if (clean.startsWith('/console/certificates/')) page = <CertDetail number={clean.split('/').pop()} />;
  else if (clean === '/console/balance') page = <BalanceList />;
  else if (clean.startsWith('/console/balance/')) page = <BalancePeriod id={clean.split('/').pop()} />;
  else if (clean.startsWith('/console/lots/') && clean.endsWith('/genealogy')) page = <Genealogy reference={clean.split('/')[3]} />;
  else if (clean.startsWith('/console/lots/')) page = <LotDetail reference={clean.split('/').pop()} />;
  else if (clean.startsWith('/console/runs/')) page = <RunDetail reference={clean.split('/').pop()} />;
  else page = <NotFound path={clean} />;

  if (isVerify || clean === '/login') {
    return <main>{page}</main>;
  }

  return (
    <div class={isConsole ? 'console' : ''}>
      <SiteHeader route={clean} console={isConsole} />
      <main>{page}</main>
      <SiteFooter />
    </div>
  );
}

render(<App />, document.getElementById('app'));
