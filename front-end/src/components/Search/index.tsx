import { useState } from 'react';
import { Button } from 'primereact/button';
import { InputText } from 'primereact/inputtext';
import pyAssistent from '../../assets/invoke';

import "primereact/resources/themes/lara-light-cyan/theme.css";
import 'primeicons/primeicons.css';
import './index.css';

function Search() {
  const [search, setSearch] = useState('');
  const [response, setResponse] = useState<string | null>(null);

  const handleSearch = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearch(event.target.value);
  };

  const handleClick = async () => {
    try {
      const result = await pyAssistent(search);
      setResponse(result);
    } catch (error) {
      console.error('Erro ao obter resposta:', error);
    }
  };

  return (
  <>
    <main className="search-container">
      <div className="input-button-group">
        <InputText
          className="input-field"
          placeholder="Pergunte aqui!"
          value={search}
          onChange={handleSearch}
        />
        <Button 
          className='search-button'
          icon="pi pi-search"
          rounded
          outlined
          severity="help"
          aria-label="Search"
          onClick={handleClick}
        />
      </div>
    </main>

    <div className="response-placeholder">
      {response ? <p className="response">{response}</p> : null}
    </div>
  </>
  );
}

export default Search;
