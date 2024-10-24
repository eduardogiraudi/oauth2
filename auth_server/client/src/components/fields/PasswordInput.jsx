import { Form } from 'react-bootstrap'
import { useState } from 'react';
import { Icon } from '@mdi/react';
import { mdiEye, mdiEyeOff } from '@mdi/js';

function PasswordInput({placeholder, value, setValue, className}) {
    const [seePassword, setSeePassword] = useState(false);
    return <div className={`password-input`}>
            <Form.Control type={seePassword ? "text" : "password"} placeholder={placeholder} value={value} onChange={(e)=>{setValue(e.target.value)}} />
            <button onClick={() => setSeePassword(!seePassword)}>
                <Icon path={seePassword ? mdiEyeOff : mdiEye} size={1} />
            </button>
            </div>


}

export default PasswordInput

