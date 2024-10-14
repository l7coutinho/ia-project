import { PrimeReactProvider } from 'primereact/api'
import Header from './components/Header'

function App() {

  return (
    <>
      <PrimeReactProvider>
        <Header />
      </PrimeReactProvider>
    </>
  )
}

export default App
