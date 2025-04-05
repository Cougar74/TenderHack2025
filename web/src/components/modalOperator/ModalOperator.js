import { Modal, Button } from 'react-bootstrap';

const ModalOperator = ({ show, handleClose }) => {
    return (
        <Modal
            show={show}
            onHide={handleClose}
            centered={true}
        >
            <Modal.Header closeButton>
                <Modal.Title>Чат с оператором</Modal.Title>
            </Modal.Header>

            <Modal.Body>Ура! Вы перешли в чат с оператором</Modal.Body>

            <Modal.Footer>
                <Button variant="primary" onClick={handleClose}>Ок</Button>
            </Modal.Footer>
        </Modal>
    );
};

export default ModalOperator;