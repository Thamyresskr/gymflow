import { Link } from "react-router-dom";

import "./Sidebar.css";

function Sidebar() {

    return (

        <aside className="sidebar">

            <h2>GymFlow</h2>

            <nav>

                <Link to="/dashboard">
                    Dashboard
                </Link>

                <Link to="/checkins">
                    Check-ins
                </Link>

                <Link to="/users">
                    Usuários
                </Link>

            </nav>

        </aside>

    );

}

export default Sidebar;