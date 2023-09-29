import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { RootLayout } from './components/RootLayout';
import { lazy, Suspense } from 'react';
import { ProtectedRoute } from './components/ProtectedRoute';
import { AuthProvider } from './contexts/UserAuthContext';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ThemeProvider } from "@/components/theme-provider"
import { AuthView } from 'src/types/enums';

const AuthPage = lazy(() => import('./pages/auth/index'));
const BillingSection = lazy(() => import('./pages/dashboard/sections/BillingSection'));
const TokenSection = lazy(() => import('./pages/dashboard/sections/TokenSection'));
const PrivacyPage = lazy(() => import('./pages/legal/Privacy'));
const TermsPage = lazy(() => import('./pages/legal/Terms'));
const HelpPage = lazy(() => import('./pages/help/index'));
const Pricing = lazy(() => import('./pages/price/index'));
const Blog = lazy(() => import('./pages/blog/Blog'));
const BlogPost = lazy(() => import('./pages/blog/BlogPost'));
const PageNotFound = lazy(() => import('./pages/404/index'));
const LandingPage = lazy(() => import('./pages/landing/index'));
const Dashboard = lazy(() => import('./pages/dashboard/index'));

const renderLoader = () => <p></p>;

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
            <Suspense fallback={renderLoader()}>
              <Routes>
                  <Route path="/" element={<LandingPage />} />
                  <Route path="/login" element={<AuthPage view={AuthView.SIGN_IN} />} />
                  <Route path="/sign-up" element={<AuthPage view={AuthView.SIGN_UP} />} />
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
                  <Route path="/blog" element={<Blog />} />
                  <Route path="/post/:slug" element={<BlogPost />} />


                  <Route path="/success" element={<Navigate to="/" />} />
                  <Route path="*" element={<PageNotFound />} />
                
              </Routes>
              </Suspense>
            </RootLayout>
          </QueryClientProvider>
        </AuthProvider>
      </BrowserRouter>
    </ThemeProvider>

  );
}

export default App;
