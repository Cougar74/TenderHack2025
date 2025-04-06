import { Table, Card } from 'react-bootstrap';

import UserRates from '../userRates/UserRates';

import './ChatElement.scss';

const ChatElement = ({ data, handleModal }) => {
    const {data_type, content, content_type, id, links} = data.Responce ? data.Responce : data;

    const generateSupport = () => {
        return(
            <span>По вашему запросу ничего не найдено. Попробуйте изменить запрос или <a href="#" onClick={handleModal}>обратитесь в поддержку</a></span>
        )
    };

    const generateLinks = () => {
        const items = links?.map((item, i) => {
            return (
                <Card.Link href={item.link} key={item.text}>{item.text}</Card.Link>
            )
        });

        return items;
    };
    
    const parse = () => {
        console.log(data_type, content, content_type, id, links);

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
            return(
                <>
                    {/* <Card style={{width: 'max-content'}} border='0'> */}
                    <Card border='0'>
                        <Card.Body className='p-0'>
                            {content ? content : generateSupport()}
                        </Card.Body>
                        {generateLinks()}
                    </Card>

                    {content ? <UserRates id={id} /> : null}
                </>
            )
        }
    };

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