# Mandarin Steps

An Android app and home-screen widget for learning Mandarin Chinese at your own pace.

- 1,000 sessions of 5 words or phrases each.
- Sessions 1–59 are a starter course covering greetings, numbers, travel and everyday phrases.
- Sessions 60–1000 cover HSK 1–6 vocabulary, with the most common words first.
- Every 7th session is a review.
- **Listen** reads each item aloud using the phone's Chinese text-to-speech voice.
- **Speak** uses Google speech recognition (zh-CN) to check your pronunciation.
- A progress tracker appears after each session and shows your streak and history.
- The home-screen widget lets you flip through words, hear them and jump into a session.

The APK is built automatically by GitHub Actions. To download it, open the **Releases** page and get `MandarinSteps.apk`.

Vocabulary comes from [complete-hsk-vocabulary](https://github.com/drkameleon/complete-hsk-vocabulary) (MIT licence). To rebuild `app/src/main/assets/sessions.tsv`, run `tools/gen_data.py`.
