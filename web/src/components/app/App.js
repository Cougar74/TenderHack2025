import { useState, useEffect, useRef } from 'react';

import { Container, Stack } from 'react-bootstrap';

import QueryInput from '../queryInput/QueryInput';
import ChatElement from '../chatElement/ChatElement';

import 'bootstrap/dist/css/bootstrap.min.css';
import './App.scss';

function App() {
    const [chatList, setChatList] = useState([]);
    const queryInputContainerRef = useRef(null);
    const lastChatElement = useRef(null);

    useEffect(() => {
        if (chatList.length === 0) {
            queryInputContainerRef.current.classList.remove('fixed-bottom');
        } else {
            queryInputContainerRef.current.classList.add('fixed-bottom');
        }
    }, [chatList]);

    const addQuery = ( query ) => {
        const data = {
            data_type: 'request',
            content: query,
            content_type: 'text',
        };

        const data_table = {
            data_type: 'response',
            content_type: 'table',
            content: {
                columns: ['#', 'Test', 'Test_2', 'Test_3'],
                values: [
                    ['1', '123', '345', '678'],
                    ['2', '223', '345', '678'],
                    ['3', '323', '345', '678'],
                ]
            },
        };

        setChatList((prevChatList) => {
            let updatedChatList;

            if (prevChatList.length === 2) {
                updatedChatList = [...prevChatList, data, data_table];
            } else {
                updatedChatList = [...prevChatList, data];
            }
            
            setTimeout(() => {
                if (lastChatElement.current) {
                    lastChatElement.current.scrollIntoView({ behavior: 'smooth' });
                }
            }, 0);

            return updatedChatList;
        });
    };

    const renderChatElement = () => {
        const items = chatList.map((chat, index) => (
            <ChatElement 
                key={index} 
                data={chat} 
                ref={index === chatList.length - 1 ? lastChatElement : null} 
            />
        ));

        return (
            <>
                {items}
            </>
        )
    }

    return (
        <>
            <Container fluid className="w-75 mt-5">
                <Stack className="position-relative mx-auto" style={{marginBottom: 108}} gap={3}>
                    {renderChatElement()}
                </Stack>
                
                <div ref={queryInputContainerRef} className="w-75 query-input-container centered">
                    <QueryInput isData={chatList.length ? true : false} addQuery={addQuery}/>
                </div>
            </Container>
        </>
    );
}

export default App;