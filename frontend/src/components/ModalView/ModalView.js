import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

function ModalView(props) {
  return (
    <Modal
      {...props}
      // size="md"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
     <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-vcenter">
          {props.modalheading}
          </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {props.modaldata}
      </Modal.Body>
    </Modal>
  );
}

export default ModalView;