import { Table, Card } from 'react-bootstrap';

import UserRates from '../userRates/UserRates';

import './ChatElement.scss';

const ChatElement = ({ data, handleModal }) => {
    const {data_type, content, content_type} = data;

    const generateSupport = () => {
        return(
            <span>По вашему запросу ничего не найдено. Попробуйте изменить запрос или <a href="#" onClick={handleModal}>обратитесь в поддержку</a></span>
        )
    }
    
    const parse = () => {
        if (data_type === 'request') {
            return (
                <Card style={{width: 'max-content', maxWidth: '75%'}} bg='body-tertiary' border='0'>
                    <Card.Body>
                        <Card.Text>
                            {content}
                        </Card.Text>
                    </Card.Body>
                </Card>
            );

        } else {
            if (content_type === 'text') {
                return (
                    <>
                        <Card style={{width: 'max-content'}} border='0'>
                            <Card.Body className='p-0'>
                                {/* {content ? content : 'По вашему запросу ничего не найдено. Попробуйте изменить запрос или обратитесь в поддержку'} */}
                                {content ? content : generateSupport()}
                            </Card.Body>
                        </Card>

                        {content ? <UserRates /> : null}
                    </>
                );
            } else {
                return (
                    generateTable(data)
                );
            }
        }
    }

    return (
        <div className={data_type === 'request' ? 'request' : 'response'}>
            {parse()}
        </div>
    );
};

const generateTable = ({ content }) => {
    const generateHeader = () => {
        const items = content.columns.map((item, i) => {
            return (
                <th>{item}</th>
            )
        });

        return (
            <tr>
                {items}
            </tr>
        )
    };

    const generateRows = () => {
        const items = content.values.map((row, i) => (
            <tr key={i}>
                {row.map((cell, j) => (
                    <td key={j}>{cell}</td>
                ))}
            </tr>
        ));
        return items;
    };

    return (
        <Table>
            <thead>
                {generateHeader()}
            </thead>

            <tbody>
                {generateRows()}
            </tbody>
        </Table>
    );
};

export default ChatElement;