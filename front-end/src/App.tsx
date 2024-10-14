import { PrimeReactProvider } from 'primereact/api'
import Header from './components/Header'
import Search from './components/Search'

function App() {

  return (
    <>
      <PrimeReactProvider>
        <Header />
        <Search />
      </PrimeReactProvider>
    </>
  )
}

export default App
