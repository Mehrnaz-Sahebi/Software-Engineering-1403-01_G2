# Text Optimization Application

A Django-based web app for Persian text optimization with user authentication and mistake tracking.

## Features
- **User Authentication**: Sign up, log in, and view user history.
- **Text Optimization**: Apply Persian text normalization (spacing, diacritics, characters, numbers, etc.).
- **Mistake Tracking**: Log and review text mistakes during optimization.
- **History**: View previous mistakes and corrections.

## Usage

- **Sign Up**: Create a new user.
- **Log In**: Log in with your username and password.
- **Optimize Text**: Submit Persian text, select normalization options, and view results.
- **View History**: Check your past mistakes and corrections.

## Functions

- `optimize_text`: Applies normalization based on user preferences.
- `find_out_mistakes`: Logs changes as mistakes in the DB.
- `fetch_user_history`: Retrieves the user's mistake history.

## Contributing

1. Fork the repo.
2. Create a new branch: `git checkout -b feature-branch`.
3. Commit and push your changes.
4. Create a pull request.

## License

MIT License - see LICENSE file for details.
