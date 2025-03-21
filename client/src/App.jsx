import { BrowserRouter, Routes, Route } from "react-router-dom"
import DataProvider from "./context/DataContext"
import LayoutGrid from "./components/LayoutGrid/LayoutGrid"
import Main from "./pages/Main/Main"
import YourDocuments from "./pages/YourDocuments/YourDocuments"
import Login from "./pages/Login/Login"
import Register from "./pages/Register/Register"
import ActivateMessage from "./pages/ActivateMessage/ActivateMessage"
import Activate from "./pages/Activate/Activate"
import Highlight from "./pages/Highlight/Highlight"

function App() {

  return (
    <BrowserRouter>

      <DataProvider>

        <LayoutGrid type='screen' />

        <Routes>

          <Route path="/" element={<Main />}>
            <Route path="login" element={<Login />} />
            <Route path="register" element={<Register />} />
            <Route path="activate-message" element={<ActivateMessage />} />
            <Route path="activate/:uidb/:token" element={<Activate />} />
            <Route path="/highlight" element={<Highlight />} />
          </Route>

          <Route path="/mydocuments" element={<YourDocuments />} />

        </Routes>

      </DataProvider>

    </BrowserRouter>
  )
}

export default App
