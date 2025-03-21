import { BrowserRouter, Routes, Route } from "react-router-dom"
import DataProvider from "./context/DataContext"
import LayoutGrid from "./components/LayoutGrid/LayoutGrid"
import Main from "./pages/Main/Main"
import YourDocuments from "./pages/YourDocuments/YourDocuments"
import Login from "./pages/Login/Login"
import Register from "./pages/Register/Register"
import Activate from "./pages/Activate/Activate"
import Highlight from "./pages/Highlight/Highlight"
import EmailMessage from "./components/EmailMessage/EmailMessage"
import ForgotPass from "./pages/ForgotPass/ForgotPass"
import Nav from "./components/Nav/Nav"
import ResetPass from "./pages/ResetPass/ResetPass"
import DocumentPage from "./pages/DocumentPage/DocumentPage"
import { GoogleOAuthProvider } from '@react-oauth/google'

function App() {

  return (
    <BrowserRouter>

      <DataProvider>

          <LayoutGrid type='screen' />

          <Nav />


          <Routes>

            <Route path="/" element={<Main />}>

              <Route path="login" element={<Login />} />
              <Route path="register" element={<Register />} />

              <Route path="activate-message" element={<EmailMessage title="Activate account" message="Click the link we sent on your email to activate your account. Log in once you're done." />} />
              <Route path="activate/:uidb/:token" element={<Activate />} />

              <Route path="forgot-pass" element={<ForgotPass />} />
              <Route path="forgot-pass-message" element={<EmailMessage title="Forgot password" message="Click the link we sent on your email to reset your password. Log in once you're done." />} />
              <Route path="reset-password/:uidb/:token" element={<ResetPass />} />

            </Route>

            
            <Route path="/mydocuments" element={<YourDocuments />} />
            <Route path="/document/:id" element={<DocumentPage />} />

          </Routes>

      </DataProvider>

    </BrowserRouter>
  )
}

export default App
