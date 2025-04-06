import { useEffect, useState } from 'react';

import { Stack, Button, InputGroup, Form } from 'react-bootstrap';

const QueryInput = ({ isData, addQuery, isLoading }) => {
    const [query, setQuery] = useState('');

    const handleSearch = () => {
        console.log('Запрос:', query);
        addQuery(query);
        setQuery('');
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !isLoading) {
            handleSearch();
        }
    };

    return (
        <Stack gap={4}>
            {isData ? null : <h2 className='text-center' style={{ caretColor: 'transparent' }}>Чем вам помочь?</h2>}
            
            <InputGroup className="mb-3">
                <Form.Control
                    placeholder="Спросите что-нибудь"
                    aria-label="Query"
                    aria-describedby="Query"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onKeyDown={handleKeyDown}
                />

                <Button
                    variant="primary"
                    disabled={isLoading}
                    onClick={!isLoading ? handleSearch : null}
                >
                    {isLoading ? 'Ожидайте...' : 'Найти'}
                </Button>
            </InputGroup>
        </Stack>
    );
};

export default QueryInput;