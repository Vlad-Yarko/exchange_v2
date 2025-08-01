import { useEffect, useState } from "react"
import { useSearchParams } from 'react-router-dom'

import api from '../../../api'


function Login() {
    const [searchParams] = useSearchParams()
    const code = searchParams.get('code')

    const [ isCode, setIsCode ] = useState(false)
    const [ variable, setVariable ] = useState(null)

    useEffect(() => {
        if (code) {
            setIsCode(true)
            const googleLogin = async () => {
                try {
                    const response = await api.post("/users/google/callback", {
                        code: code
                    })
                    setVariable(JSON.stringify(response.data))
                } catch (error) {
                    console.log("DKKDKDKDKD", error)
                    setIsCode(false)
                }
            }
            googleLogin()
        } else {
            setIsCode(false)
        }

    }, [code])

    return (
			<>
				{isCode ? (
					variable ? (
						<div>
							<h1>{variable}</h1>
						</div>
					) : (
						<div>
							<h1>Processing...</h1>
						</div>
					)
				) : (
					<div>
						<h1>Code has not found</h1>
					</div>
				)}
			</>
		)
}


export default Login
