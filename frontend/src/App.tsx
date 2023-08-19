import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import RootLayout from './components/RootLayout';

import WelcomePage from './pages/WelcomePage';
import { CustomProvider } from 'rsuite';
import Login from './pages/Login';
import ProtectedRoute from './components/ProtectedRoute';
import { AuthProvider } from './hooks/Auth';
import { loadStripe } from '@stripe/stripe-js';
import { useEffect, useState } from 'react';
import { Elements } from '@stripe/react-stripe-js';
import PageNotFound from './pages/PageNotFound';
import Dashboard from './pages/Dashboard';
import BillingSection from './pages/dashboard-sections/BillingSection';
import TokenSection from './pages/dashboard-sections/TokenSection';
import {
  useQuery,
  useMutation,
  useQueryClient,
  QueryClient,
  QueryClientProvider,
} from '@tanstack/react-query'
import { ThemeProvider } from "@/components/theme-provider"



const queryClient = new QueryClient()

function App() {


  const [clientSecret, setClientSecret] = useState("");

  // useEffect(() => {
  //   // Create PaymentIntent as soon as the page loads
  //   fetch("/create-payment-intent", {
  //     method: "POST",
  //     headers: { "Content-Type": "application/json" },
  //     body: JSON.stringify({ items: [{ id: "xl-tshirt" }] }),
  //   })
  //     .then((res) => res.json())
  //     .then((data) => setClientSecret(data.clientSecret));
  // }, []);

  const appearance = {
    theme: 'stripe',
  };
  const options = {
    clientSecret,
    appearance,
  };



  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <BrowserRouter>
        <AuthProvider>
          <QueryClientProvider client={queryClient}>
            <RootLayout>
              <Routes>
                <Route
                  path="/protected"
                  element={
                    <ProtectedRoute>
                      <WelcomePage />
                    </ProtectedRoute>
                  }
                />
                <Route path="/" element={<WelcomePage />} />
                <Route path="/login" element={<Login />} />
                <Route
                  path="/billing"
                  element={
    
                      // <Elements stripe={stripePromise}>
                      //   <CheckoutForm />
                      // </Elements>

                      <BillingSection></BillingSection>
                    
                  
                  }
                >
                  {/* <Route index element={<BlogPostsPage />} />
                  <Route path=":id" element={<PostDetailPage />} /> */}
                </Route>
                {/* <Route path="/blog/new" element={<NewPostPage />} /> */}
                <Route path="/dashboard" element={<Dashboard />} >
                  <Route index path="billing" element={<BillingSection/>}/>
                  <Route index path="token" element={<TokenSection/>}/>
                </Route>
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
