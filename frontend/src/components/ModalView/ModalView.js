import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

function ModalView(props) {
  return (
    <Modal
      {...props}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
     <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-vcenter">
          {props.modalHeading}
          </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {props.modalData}
      </Modal.Body>
      <Modal.Footer>
          <Button onClick={props.onHide}>Close</Button>
      </Modal.Footer>
    </Modal>
  );
}

export default ModalView;