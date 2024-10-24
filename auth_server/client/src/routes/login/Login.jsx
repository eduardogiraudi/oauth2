import PasswordInput from "@components/fields/PasswordInput"
import { useState } from "react"

function Login() {
    const [password, setPassword] = useState('')
    return <PasswordInput value={password} setValue={setPassword} placeholder="password"/>
}

export default Login