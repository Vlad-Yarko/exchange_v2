// import { useNavigate } from 'react-router-dom'

import API_DOMAIN from '../../../constants/api'

import './Home.css'


function Home() {
    // const navigate = useNavigate()

    const handleLogin = () => {
        const uri = `http://${API_DOMAIN}/users/google/url`
        window.location.href = uri
    }

    return (
        <>
            <div>
                <h1>Home</h1>
                <button onClick={handleLogin}>Oauth 2.0</button>
            </div>
        </>
    )
}


export default Home
