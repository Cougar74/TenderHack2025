import { useState, useEffect, use } from 'react';
import { Card } from 'react-bootstrap';

import Rate_1 from '../../icons/1.png';
import Rate_2 from '../../icons/2.png';
import Rate_3 from '../../icons/3.png';
import Rate_4 from '../../icons/4.png';
import Rate_5 from '../../icons/5.png';

import './UserRates.scss';

const UserRates = (rate) => {
    const [activeItem, setActiveItem] = useState(rate);
    const data = [ Rate_1, Rate_2, Rate_3, Rate_4, Rate_5];

    const changeActive = (value) => {
        console.log('New Rate: ', value);
        setActiveItem(value);
    };

    const renderEmoji = () => {
        return data.map((emoji, index) => (
            <UserRatesItem key={index} emoji={emoji} changeActive={changeActive} value={index + 1} isActive = {activeItem === index + 1 ? true : false}/>
        ));
    };

    return (
        <Card style={{width: 'max-content'}} border='0'>
            <Card.Body className='p-0'>
                <div className="userRates">
                    <span>
                        Вы довольны ответом?
                    </span>

                    <div className="userRatesEmoji">
                        {renderEmoji()}
                    </div>
                </div>
            </Card.Body>
        </Card>
    );
};

const UserRatesItem = ({ emoji, value, changeActive, isActive = false }) => {
    const [color, setColor] = useState('');

    const handleClick = () => {
        changeActive(value);
        generateColor();
    };

    useEffect(() => generateColor(), [isActive]);

    const generateColor = () => {
        if (!isActive) {
            setColor('');
            return;
        }

        switch (value) {
            case 1:
                setColor('item-red');
                break;

            case 2:
                setColor('item-orange');
                break;

            case 3:
                setColor('item-yellow');
                break;

            case 4:
                setColor('item-grass');
                break;

            case 5:
                setColor('item-green');
                break;

            default:
                setColor('')
                break;
        }
    };
    
    return (
        <div className={`userRatesEmojiItem ${color}`} onClick={handleClick}>
            <img src={emoji} />
        </div>
    )
};

export default UserRates;