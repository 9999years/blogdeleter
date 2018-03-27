[CmdletBinding()]

<#
.PARAMETER File
File of URLs to delete; one per-line. Like:
	staff
	blog
	etc
i.e. without https:// or .tumblr.com/
#>
Param(
	[String]$File
)

Get-Content $File | %{
	$url = $_
	$ret = .\blogdeleter.py $url
	If($ret -ne "Deleting $url... success!") {
		throw $ret
	} Else {
		$ret
	}
}
