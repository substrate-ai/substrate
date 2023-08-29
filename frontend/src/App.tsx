import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import RootLayout from './components/RootLayout';

import WelcomePage from './pages/Welcome';
import ProtectedRoute from './components/ProtectedRoute';
import { AuthProvider } from './hooks/Auth';
import PageNotFound from './pages/PageNotFound';
import Dashboard from './pages/Dashboard';
import BillingSection from './pages/dashboard-sections/BillingSection';
import TokenSection from './pages/dashboard-sections/TokenSection';
import {
  QueryClient,
  QueryClientProvider,
} from '@tanstack/react-query'
import { ThemeProvider } from "@/components/theme-provider"
import Pricing from './pages/Pricing';
import TermsPage from './pages/legal/Terms';
import PrivacyPage from './pages/legal/Privacy';
import HelpPage from './pages/Help';
import { AuthPage, View } from './pages/AuthPage';



const queryClient = new QueryClient()

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
                  <Route index path="billing" element={<BillingSection/>}/>
                  <Route path="token" element={<TokenSection/>}/>
                </Route>
                <Route path="legal">
                  <Route path="terms-and-conditions" element={<TermsPage />} />
                  <Route path="privacy-policy" element={<PrivacyPage />} />
                </Route>
                <Route path="contact" element={<HelpPage/>} />

                <Route path="/pricing" element={<Pricing/>}/>
                <Route path="/404" element={<PageNotFound />} />
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
