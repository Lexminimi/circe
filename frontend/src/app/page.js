//link to the tutorial: https://dev.to/koladev/building-a-fullstack-application-with-django-django-rest-nextjs-3e26
"use client";
import Image from "next/image";
import styles from "./page.module.css";
import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";

async function getData() {
  const username = 'reka';
  const password = 'B1a9l8i8'; // **Important:** Consider storing credentials securely (environment variables, etc.)

  // Encode username and password for basic auth
  const encodedCredentials = btoa(`${username}:${password}`);
  const authorizationHeader = `Basic ${encodedCredentials}`;

  try {
    const response = await fetch("https://fischerb2.pythonanywhere.com/group/1", {
      headers: {
        Authorization: authorizationHeader,
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch data: ${response.status}`); // Include status code for debugging
    }

    return await response.json();
  } catch (error) {
    console.error("Error fetching data:", error);
    // Handle errors appropriately, e.g., display an error message to the user
  }
}

const MenuItem = ({ id, name}) => {
  return (
    <div className="menu-item" data-id={id}>
      <div className="menu-item-info">
        <div className="menu-item-name">{name}</div>
      </div>
    </div>
  );
};

export default function Page() {
  const [menuItems, setMenuItems] = useState(null);
  const router = useRouter();
  const params = useSearchParams();

  // State for displaying a success message
  const [displaySuccessMessage, setDisplaySuccessMessage] = useState({
    show: false,
    type: "", // either 'add' or 'update'
  });

  // Fetch menu items on component mount
  useEffect(() => {
    const fetchData = async () => {
      const data = await getData();
      setMenuItems(data);
    };
    fetchData().catch(console.error);
  }, []);

  // Detect changes in URL parameters for success messages
  useEffect(() => {
    if (!!params.get("action")) {
      setDisplaySuccessMessage({
        type: params.get("action"),
        show: true,
      });
      router.replace("/");
    }
  }, [params, router]);

  // Automatically hide the success message after 3 seconds
  useEffect(() => {
    const timer = setTimeout(() => {
      if (displaySuccessMessage.show) {
        setDisplaySuccessMessage({ show: false, type: "" });
      }
    }, 3000);
    return () => clearTimeout(timer);
  }, [displaySuccessMessage.show]);

  // Handle deletion of a menu item
  const handleDelete = (id) => {
    setMenuItems((items) => items.filter((item) => item.id !== id));
  };

  return (
    <div>
      {menuItems ? (
        menuItems.map((item) => (
          <MenuItem
            key={item.id}
            id={item.id}
            name={item.name}
          />
        ))
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}
