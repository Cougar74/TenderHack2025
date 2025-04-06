import { useState, useEffect, useRef } from 'react';
import { Container, Stack, Button } from 'react-bootstrap';

import useApiService from '../../services/ApiService';

import QueryInput from '../queryInput/QueryInput';
import ChatElement from '../chatElement/ChatElement';
import ModalOperator from '../modalOperator/ModalOperator';

import 'bootstrap/dist/css/bootstrap.min.css';
import './App.scss';

function App() {
    const [chatList, setChatList] = useState([]);
    const queryInputContainerRef = useRef(null);
    const lastChatElement = useRef(null);
    const [showModal, setShowModal] = useState(false);
    const {loading, error, getUserHistory, postQueryResponse, clearError} = useApiService();

    const onHistoryLoaded = (history) => {
        setChatList(history);
    };

    const getUuid = () => {
        let uuid = localStorage.getItem('uuid');

        if (!uuid) {
            uuid = crypto.randomUUID();
            localStorage.setItem('uuid', uuid);
        }

        return uuid;
    };

    useEffect(() => {
        const uuid = getUuid();

        clearError();
        getUserHistory(uuid)
            .then(onHistoryLoaded);
    }, []);

    useEffect(() => {
        if (chatList.length === 0) {
            queryInputContainerRef.current.classList.remove('fixed-bottom');
        } else {
            queryInputContainerRef.current.classList.add('fixed-bottom');
        }
    }, [chatList]);

    const handleClose = () => setShowModal(false);
    const handleShow = () => setShowModal(true);

    const updateChatList = ( new_data ) => {
        setChatList((prevChatList) => ([...prevChatList, new_data]));
    };

    const addQuery = ( query ) => {
        const data = {
            data_type: 'request',
            content: query,
            content_type: 'text',
        };
        updateChatList(data);

        clearError();
        postQueryResponse(query)
            .then(({ id, answer, links }) => {
                const data = {
                    data_type: 'response',
                    content: answer,
                    content_type: 'text',
                    id: id,
                    links: links,
                };

                updateChatList(data);
            });
    };

    const generateNewDialog = () => {
        const uuid = crypto.randomUUID();
        localStorage.setItem('uuid', uuid);

        setChatList([]);
    };

    const renderChatElement = () => {
        const items = chatList.map((chat, index) => (
            <ChatElement 
                key={index} 
                data={chat}
                handleModal={handleShow}
                ref={index === chatList.length - 1 ? lastChatElement : null} 
            />
        ));

        return (
            <>
                {items}
                {chatList.length ?
                    <Button
                        variant="secondary"
                        onClick={generateNewDialog}
                        style={{ width: 'max-content'}}
                    >
                        Начать новый диалог
                    </Button> : null
                }
            </>
        )
    };

    return (
        <>
            <Container fluid className="w-75 mt-5">
                <Stack className="position-relative mx-auto" style={{marginBottom: 108}} gap={3}>
                    {renderChatElement()}
                </Stack>
                
                <div ref={queryInputContainerRef} className="w-75 query-input-container centered">
                    <QueryInput isData={chatList.length ? true : false} addQuery={addQuery} isLoading={loading}/>
                </div>
            </Container>

            {showModal ? <ModalOperator show={showModal} handleClose={handleClose}/> : null}
        </>
    );
}

export default App;