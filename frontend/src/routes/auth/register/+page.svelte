<script lang="ts">
	import PostView from './../../../lib/components/postView.svelte';

	let email = '',
		password = '',
		repeatedPassword = '',
		firstname = '',
		lastname = '',
		error = '';

	export let form;
	export let data;
</script>

<form method="POST">
	<div class="root">
		<div class="container">
			<div class="left">
				<h2>Sign in</h2>
				<div class="content">
					<div class="inputs">
						<input
							name="firstname"
							type="text"
							id="firstname"
							placeholder="Name"
							bind:value={firstname}
						/>
						<input
							name="lastname"
							type="text"
							id="lastname"
							placeholder="Lastname"
							bind:value={lastname}
						/>
						<input name="email" type="text" id="email" placeholder="Email" bind:value={email} />
						<input
							name="password"
							type="password"
							id="password"
							placeholder="Password"
							bind:value={password}
						/>
						<input
							name="repeatPassword"
							type="password"
							id="repeatPassword"
							placeholder="Repeat Password"
							bind:value={repeatedPassword}
						/>
					</div>
					<div class="errorslot">
						{#if password !== repeatedPassword}
							<small style="color: var(--font-error-color)};">Password do not match!</small>
						{/if}
						{#if form?.error}
							<small style="color: {form?.state};">{form?.error}</small>
						{/if}
					</div>
					<!-- <div class="oauth">
						<b>Continue with:</b>
						<button>G</button>
					</div> -->
				</div>
				<div class="ralign">
					{#if password !== repeatedPassword || !email || !password || !firstname || !lastname}
						<button type="submit" disabled>Sign in</button>
					{:else if password === repeatedPassword || email || password || firstname || lastname}
						<button type="submit">Sign in</button>
					{/if}
				</div>
			</div>
			<div class="right">
				<PostView post={data.latest_post} imageOnly={true} useAnalytics={false}></PostView>
			</div>
		</div>
	</div>
</form>

<style>
	.root {
		padding: 25px;
		display: flex;
		justify-content: center;
		align-items: center;
	}
	.container {
		padding: 0px;
		width: unset;
		height: fit-content;
		border-radius: var(--border-radius-heavy);
		border: 2px solid var(--border-color);
		background-color: var(--background-blurry);
		display: flex;
		flex-direction: row;
		overflow: hidden;
	}
	.container > .left {
		padding: 1rem;
		width: 40%;
		min-width: 250px;
		display: flex;
		flex-direction: column;
		gap: 10px;
	}
	.container > .right {
		width: unset;
		display: flex;
		align-items: center;
		padding: 1rem;
	}
	.left > .content {
		height: 100%;
		display: flex;
		flex-direction: column;
		gap: 20px;
		align-items: unset;
		justify-self: unset;
	}
	.left > .content > .errorslot {
		height: 0px;
		transform: translateY(-12.5px);
	}
	.left > .content > .inputs {
		display: flex;
		flex-direction: column;
		gap: 20px;
	}
	.left > .content > .oauth {
		display: flex;
		flex-direction: column;
		gap: 20px;
	}
	.left h3 {
		margin: 15px;
	}
	.ralign {
		display: flex;
		justify-content: right;
		align-items: center;
	}
	@media screen and (max-width: 1200px) {
		.root {
			display: flex;
			flex-direction: row;
			overflow: hidden;
			width: unset;
			margin-left: 2rem;
			margin-right: 2rem;
		}
	}
	@media screen and (max-width: 1000px) {
		/* .right{
		display: none;
	} */
	}
	@media screen and (max-width: 720px) {
		.root {
			margin-left: 0.5rem;
			margin-right: 0.5rem;
		}
		.right {
			display: none !important;
		}
		.container {
			width: 100%;
		}
		.left {
			width: 100% !important;
		}
	}
</style>
