import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import RootLayout from './components/RootLayout';

import WelcomePage from './pages/Welcome';
import ProtectedRoute from './components/ProtectedRoute';
import { AuthProvider } from './hooks/Auth';
import PageNotFound from './pages/PageNotFound';
import Dashboard from './pages/Dashboard';
import {
  QueryClient,
  QueryClientProvider,
} from '@tanstack/react-query'
import { ThemeProvider } from "@/components/theme-provider"
import Pricing from './pages/Pricing';
import HelpPage from './pages/Help';
import { AuthPage, View } from './pages/AuthPage';
import loadable from '@loadable/component';
import pMinDelay from 'p-min-delay';
import Blog from './pages/Blog';
import BlogPost from './pages/BlogPost';

// todo I think component are reloaded when navigating to a new page

const fallback = <h1>Loading</h1>

const minDelay = 200;

const BillingSection = loadable(() =>
  pMinDelay(import('./pages/dashboard-sections/BillingSection'), minDelay),
  { fallback }
);

const TokenSection = loadable(() =>
  pMinDelay(import('./pages/dashboard-sections/TokenSection'), minDelay),
  { fallback }
);

const TermsPage = loadable(() =>
  pMinDelay(import('./pages/legal/Terms'), minDelay),
  { fallback }
);

const PrivacyPage = loadable(() =>
  pMinDelay(import('./pages/legal/Privacy'), minDelay),
  { fallback }
);


const queryClient = new QueryClient(
  {
    defaultOptions: {
      queries: {
        retry: false,
        refetchOnWindowFocus: false,
      },
    }
  }
)

function App() {

  // if user is logged in, redirect to dashboard

  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <BrowserRouter>
        <AuthProvider>
          <QueryClientProvider client={queryClient}>
            <RootLayout>
              <Routes>
                <Route path="/" element={<WelcomePage />} />
                <Route path="/login" element={<AuthPage view={View.SIGN_IN} />} />
                <Route path="/sign-up" element={<AuthPage view={View.SIGN_UP} />} />
                <Route path="/dashboard" element={
                  <ProtectedRoute>
                      <Dashboard />
                  </ProtectedRoute>
                } >
                  <Route path="billing" element={<BillingSection />}/>
                  <Route path="token" element={<TokenSection/>}/>
                </Route>
                <Route path="legal">
                  <Route path="terms-and-conditions" element={<TermsPage />} />
                  <Route path="privacy-policy" element={<PrivacyPage />} />
                </Route>
                <Route path="contact" element={<HelpPage/>} />

                <Route path="/pricing" element={<Pricing/>}/>
                <Route path="/404" element={<PageNotFound />} />
                <Route path="/blog" element={<Blog />} />
                <Route path="/post/:slug" element={<BlogPost />} />


                <Route path="/success" element={<Navigate to="/" />} />
                <Route path="*" element={<Navigate to="/404" />} />
              </Routes>
            </RootLayout>
          </QueryClientProvider>
        </AuthProvider>
      </BrowserRouter>
    </ThemeProvider>

  );
}

export default App;
