import { BrowserRouter, Route, Routes } from "react-router-dom";
import LandingPage from "./page/LandingPage";
import PricingPage from "./page/PricingPage";
import DocsPage from "./page/DocsPage";
import AuthPage from "./page/AuthPage";
import { useEffect, useState } from "react";
import { AuthProvider } from "./supabase/AuthProvider";
import RootLayout from "./component/RootLayout";
import ProtectedRoute from "./component/ProtectedRoute";
import DashboardPage from "./page/DashboardPage";



export default function App() {


  return (
    // <div className="h-screen bg-gradient-to-br from-gray-900 to-gray-600 bg-gradient-to-r text-gray-100 ">
    //     <RouterProvider router={router} />
    // </div>    
    <BrowserRouter>
    <AuthProvider>
      <RootLayout>
        <Routes>
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <DashboardPage />
              </ProtectedRoute>
            }
          />
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<AuthPage />} />
        </Routes>
      </RootLayout>
    </AuthProvider>
  </BrowserRouter>
  )
}