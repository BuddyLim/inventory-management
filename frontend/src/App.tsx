import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import './reset.css'
import './App.css'
import InventoryForm from './components/inventoryForm'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
     <InventoryForm/>
    </>
  )
}

export default App
