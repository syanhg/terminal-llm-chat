# Setting Up GitHub Pages

Follow these steps to enable GitHub Pages for the Terminal LLM Chat website:

1. Go to your repository on GitHub
2. Click on "Settings"
3. In the left sidebar, click on "Pages"
4. Under "Source", select "Deploy from a branch"
5. Under "Branch", select "main" and "/docs" folder
6. Click "Save"

After a few minutes, your site will be published at: https://syanhg.github.io/terminal-llm-chat/

## Custom Domain (Optional)

If you want to use a custom domain:

1. In the GitHub Pages settings, under "Custom domain", enter your domain name
2. Click "Save"
3. Add the following DNS records with your domain registrar:
   - Type: A, Name: @, Value: 185.199.108.153
   - Type: A, Name: @, Value: 185.199.109.153
   - Type: A, Name: @, Value: 185.199.110.153
   - Type: A, Name: @, Value: 185.199.111.153
   - Type: CNAME, Name: www, Value: syanhg.github.io

4. Wait for DNS propagation (may take up to 24 hours)
5. Check "Enforce HTTPS" in the GitHub Pages settings once your certificate is ready

## Troubleshooting

If your site doesn't publish:

1. Make sure the index.html file is in the root of your docs folder
2. Check for any build errors in the GitHub Actions tab
3. Wait a few minutes as GitHub Pages deployment can take some time
4. If using a custom domain, verify your DNS settings are correct