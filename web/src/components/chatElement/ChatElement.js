import { Table, Card } from 'react-bootstrap';

import './ChatElement.scss';

const ChatElement = ({ data }) => {
    const {data_type, content, content_type} = data;
    
    const parse = () => {
        
        if (data_type === 'request') {
            return (
                <Card style={{width: 'max-content', maxWidth: '75%'}} bg='body-tertiary' border='0'>
                    <Card.Body>
                        {content}
                    </Card.Body>
                </Card>
            );

        } else {
            if (content_type === 'text') {
                return (
                    <Card style={{width: 'max-content', maxWidth: '75%'}} bg='body-tertiary' border='0'>
                        <Card.Body>
                            {content}
                        </Card.Body>
                    </Card>
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