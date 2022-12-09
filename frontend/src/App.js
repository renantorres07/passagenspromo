import "bootstrap/dist/css/bootstrap.min.css"
import "./App.css"
import { BrowserRouter, Routes, Route } from "react-router-dom"
import AirportTable from "./components/AirportTable"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/airports" element={<AirportTable />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App