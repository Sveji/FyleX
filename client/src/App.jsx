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

          <Route path="/" element={<Main />} />
          <Route path="/highlight" element={<Highlight />} />


        </Routes>

      </DataProvider>

    </BrowserRouter>
  )
}

export default App
