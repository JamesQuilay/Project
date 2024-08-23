<?php

class Session
{
    // Start the session if it hasn't been started
    public static function start()
    {
        if (session_status() == PHP_SESSION_NONE) {
            session_start();
        }
    }

    // Set session data
    public static function set($key, $value)
    {
        self::start();
        $_SESSION[$key] = $value;
    }

    // Get session data
    public static function get($key)
    {
        self::start();
        return isset($_SESSION[$key]) ? $_SESSION[$key] : null;
    }

    // Set the current logged-in user data in session
    public static function setUser($user)
    {
        self::set('user', $user);
    }

    // Get the current logged-in user data from session
    public static function getUser()
    {
        return self::get('user');
    }

    // Destroy the session and log the user out
    public static function destroy()
    {
        self::start();
        session_unset();    // Unset all session variables
        session_destroy();  // Destroy the session
    }
}
