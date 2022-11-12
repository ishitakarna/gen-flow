import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

function DeleteModal(props) {
    function handleDeleteWorkflowInst() {
        props.onHide();
    }

    return (
        <>
        <h5>All data associated with this workflow instance will be deleted.</h5>
        <h6>Are you sure you want to delete?</h6>
        <Modal.Footer>
          <Button onClick={handleDeleteWorkflowInst}>{"Delete"}</Button>
        </Modal.Footer>
        </>
    )
}

export default DeleteModal;