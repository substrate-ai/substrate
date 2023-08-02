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

const stripePromise = loadStripe("pk_test_51NTikzIaSQMc4h1thj38McKyOeLfJOGobRJe1oMhrZOeZziVl2Cy8wLfCJsa2yWxh9USLT8do0VXEFUq6BYOapuA001nSVIu1z");


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
    <CustomProvider theme="dark">
      <BrowserRouter>
        <AuthProvider>
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
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/404" element={<PageNotFound />} />
          	  <Route path="*" element={<Navigate to="/404" />} />
            </Routes>
          </RootLayout>
        </AuthProvider>
      </BrowserRouter>
    </CustomProvider>
  );
}

export default App;
